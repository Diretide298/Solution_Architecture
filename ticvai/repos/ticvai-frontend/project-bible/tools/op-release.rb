# The release push: one idempotent run that brings OpenProject project 153 in line with one release bundle
# (OpenProject 10.0.2, Docker container "openproject", Ruby 2.6 / Rails 5.2). Council items C6 and C7.
#
# It replaces the chain op-create.rb, op-created-merge, op-descriptions.rb MODE=status, op-order-sync.rb,
# op-bulk-links.rb, op-assign-sync.rb, op-retire.py and op-check.rb (all still in tools/, unchanged). The bundle is
# handoff/service-docs/op-release.json, built by tools/op-release.py at the release tag and committed with it.
#
# Dry run by default: every phase prints its full plan (the first SHOW=40 lines of each list; SHOW=all for all).
# APPLY=1 applies the phases in this order, each in one transaction, with no mail (notifications off):
#
#   guard         refuses to run if two keys map to one OpenProject id, or a pushed plan ticket is missing
#   create        tickets with no id yet, parents before children; an existing ticket with the same subject under
#                 the same parent (and no key of its own) is taken, not made again. A New plan ticket under the
#                 wrong parent is moved under the plan's. Writes /tmp/op-created.json {key: id} (CREATED_OUT).
#   guard again   with the new ids
#   priority      Priority_No. (the build order) on every plan ticket, started and closed ones too
#   assign        assignee, accountable, Block A week on New tickets (names through the bundle's aliases); a
#                 started ticket gets one comment per release naming the plan's person (ASSIGN_COMMENT=0: none)
#   links         removes a direct follows link between two plan tasks the plan no longer orders (even through a
#                 chain), then adds the missing ones; duplicates are skipped
#   retire        tickets that left the plan: on hold (defer) or rejected (merge), with the reason as a comment,
#                 New tickets only; the unexplained ones are listed and never touched
#   descriptions  pointer bodies (C7): a New ticket's description becomes its pointer; a started ticket keeps its
#                 text and gets ONE comment that its spec lives in ADAM (found again by its wording, so never
#                 twice); New tickets are retitled to the plan (RETITLE=all: started ones too).
#                 BATCH=n: at most n rewrites and n comments this run, earliest build order first
#   health        read-only summary in the style of op-check.rb
#
# ONLY=phase,phase runs just those (guard always runs), e.g. ONLY=descriptions BATCH=200 for the staged pointers.
# AUTHOR=<login or email> if Chinmay Parab's account is not found by name. EXPECT_RELEASE=r1 refuses any other bundle.
# LIMIT=n adds only n links (to time them). Back up the database first (OPENPROJECT-PUSH.md).
#
#   docker cp tools/op-release.rb openproject:/tmp/ && docker cp handoff/service-docs/op-release.json openproject:/tmp/
#   dry run:  docker exec openproject bash -c 'cd /app && bundle exec rails runner /tmp/op-release.rb /tmp/op-release.json'
#   apply:    docker exec -e APPLY=1 openproject bash -c 'cd /app && bundle exec rails runner /tmp/op-release.rb /tmp/op-release.json'
#   tools/op-release-server.sh does all of this from the server's git checkout.
#
# Written for Ruby 2.6: no .tally, .filter_map or numbered block parameters.

require "json"
require "set"

path = ARGV[0] or abort("usage: rails runner op-release.rb op-release.json")
B = JSON.parse(File.read(path))
APPLY = ENV["APPLY"] == "1"
SHOW = ENV["SHOW"] == "all" ? nil : (ENV["SHOW"] || "40").to_i
BATCH = ENV["BATCH"].to_s =~ /\A\d+\z/ ? ENV["BATCH"].to_i : nil
LINK_LIMIT = ENV["LIMIT"].to_s =~ /\A\d+\z/ ? ENV["LIMIT"].to_i : nil
PHASES = %w[create priority assign links retire descriptions health].freeze
ONLY = ENV["ONLY"] ? ENV["ONLY"].split(",").map(&:strip).reject(&:empty?) : PHASES
PROJECT_ID = B["project"].to_i
RELEASE = B["release"].to_s
CREATED_OUT = ENV["CREATED_OUT"] || "/tmp/op-created.json"
POINTER_PREFIX = B["markers"]["pointer"]
RELEASE_PREFIX = B["markers"]["release"]
COMMENT_MARKER = B["markers"]["comment"]
ASSIGN_MARKER = "Plan update (release #{RELEASE})"

def rel_say(line = "")
  puts line
  $stdout.flush
end

def rel_list(list)
  shown = SHOW ? list.first(SHOW) : list
  shown.each { |l| rel_say "    #{l}" }
  rel_say "    ... and #{list.size - shown.size} more (SHOW=all lists every one)" if list.size > shown.size
end

def rel_phase(name)
  rel_say ""
  rel_say "== #{name} #{APPLY ? '(APPLY)' : '(dry run)'} " + ("=" * [4, 64 - name.size].max)
end

def rel_run?(name)
  ONLY.include?(name)
end

# No mail for anything this run writes. OpenProject 10 has Journal::NotificationConfiguration; older ones do not.
def rel_quietly
  if defined?(Journal::NotificationConfiguration)
    Journal::NotificationConfiguration.with(false) { yield }
  else
    yield
  end
end

def rel_count_by(list)
  out = Hash.new(0)
  list.each { |x| out[yield(x)] += 1 }
  out
end

unknown_phases = ONLY - PHASES
abort("ONLY names unknown phases: #{unknown_phases.join(', ')} (phases: #{PHASES.join(', ')})") if unknown_phases.any?
abort("not a release bundle: no release tag in #{path}") unless RELEASE =~ /\Ar\d+\z/
if ENV["EXPECT_RELEASE"] && ENV["EXPECT_RELEASE"] != RELEASE
  abort("REFUSED: the bundle is for #{RELEASE}, the checkout is #{ENV['EXPECT_RELEASE']}; rebuild it at the tag")
end

project = Project.find_by(id: PROJECT_ID) or abort("project #{PROJECT_ID} not found")
# Everything this writes is authored by Chinmay Parab, never by whichever account is the instance admin (on
# 30 September tickets made with an "admin" fallback showed up under Sameer Shinde). Nothing falls back.
author = (ENV["AUTHOR"] && (User.find_by(login: ENV["AUTHOR"]) || User.find_by(mail: ENV["AUTHOR"]))) ||
         User.active.detect { |u| u.name == (B["author"] || "Chinmay Parab") }
abort("author not found: no active user named #{B['author']}; run with AUTHOR=<his login>") unless author

aliases = B["aliases"] || {}
users = {}
User.active.to_a.each { |u| users[u.name] = u }
find_user = lambda do |name|
  next nil if name.nil? || name.empty?
  users[aliases[name] || name] || users[name]
end
version_col = WorkPackage.column_names.include?("version_id") ? :version_id : :fixed_version_id

st = B["statuses"]
NEW_ID = st["new"].to_i
status_new = Status.find_by(id: NEW_ID)
status_hold = Status.find_by(id: st["on_hold"])
status_rejected = Status.find_by(id: st["rejected"])
unless status_new && status_hold && status_rejected
  abort("statuses not found: new ##{st['new']}, on hold ##{st['on_hold']}, rejected ##{st['rejected']}")
end

ids = {}
B["ids"].each { |k, v| ids[k] = v.to_i }
tickets = B["tickets"]
by_key = {}
tickets.each { |t| by_key[t["key"]] = t }
left_ids = (B["retire"].map { |e| e["id"] } + B["unexplained"].map { |e| e["id"] }).compact.map(&:to_i).to_set

rel_say "OpenProject #{OpenProject::VERSION}: release #{RELEASE} bundle, built from #{B['built_from']} at #{B['built_at']}"
rel_say "project ##{PROJECT_ID} #{project.name}; author #{author.name}; statuses: New = #{status_new.name}, " \
    "defer = #{status_hold.name}, merge = #{status_rejected.name}"
rel_say "#{APPLY ? 'APPLY' : 'DRY RUN (APPLY=1 applies)'}; phases: #{ONLY.join(', ')}" +
    (BATCH ? "; BATCH=#{BATCH}" : "") + (LINK_LIMIT ? "; LIMIT=#{LINK_LIMIT}" : "")
rel_say "bundle: #{tickets.size} plan tickets, #{ids.size} pushed ids, #{B['create'].size} to create, " \
    "#{B['links'].size} links, #{B['retire'].size} leaving the plan, #{B['unexplained'].size} unexplained"

# ---------------------------------------------------------------------------------------------------------- guard
# Two keys on one ticket put one task's links and text on another's (30 September, SVC-WALLET-RETAIL-1/-2).
guard = lambda do |map, label|
  by_id = Hash.new { |h, k| h[k] = [] }
  map.each { |k, i| by_id[i] << k if i.is_a?(Integer) }
  shared = by_id.select { |_, ks| ks.size > 1 }
  next if shared.empty?
  shared.first(20).each { |i, ks| rel_say "  ##{i}: #{ks.sort.join(', ')}" }
  abort("REFUSED (#{label}): #{shared.size} OpenProject ids are mapped to more than one key. Repair pms-map.json " \
        "and rebuild the bundle; nothing more was written")
end

rel_phase("guard")
guard.call(ids, "before create")
plan_ids = tickets.map { |t| ids[t["key"]] }.compact
project_of = WorkPackage.where(id: plan_ids).pluck(:id, :project_id).to_h
missing = plan_ids.reject { |i| project_of.key?(i) }
foreign = plan_ids.select { |i| project_of.key?(i) && project_of[i] != PROJECT_ID }
key_of = ids.invert
if missing.any? || foreign.any?
  rel_list(missing.map { |i| "missing ##{i} #{key_of[i]}" } + foreign.map { |i| "not in project: ##{i} #{key_of[i]}" })
  abort("REFUSED: #{missing.size} plan tickets in pms-map.json are not in OpenProject, #{foreign.size} are in " \
        "another project. Take them out of pms-map.json (the bundle then makes them again) and rebuild")
end
rel_say "ok: #{ids.size} keys, #{ids.values.uniq.size} distinct ids; all #{plan_ids.size} pushed plan tickets are in the project"

created = {}      # key -> id made or taken in this run; :pending in a dry run for one still to make
resolve = lambda { |k| ids[k] || created[k] }
results = []

# --------------------------------------------------------------------------------------------------------- create
if rel_run?("create")
  rel_phase("create")
  owned = ids.values.to_set
  claimed = Set.new
  steps = []
  B["create"].each do |k|
    t = by_key[k] or abort("create lists #{k}, which has no ticket entry in the bundle")
    pk = t["parent"]
    parent_id = pk ? resolve.call(pk) : nil
    abort("#{k}: its parent #{pk} has no ticket and is not made earlier in this run") if pk && parent_id.nil?
    found = nil
    if parent_id.is_a?(Integer)
      found = WorkPackage.find(parent_id).children.where(subject: t["subject"]).order(:id).to_a
                         .detect { |w| !owned.include?(w.id) && !claimed.include?(w.id) }
    elsif pk.nil?
      found = WorkPackage.where(project_id: PROJECT_ID, subject: t["subject"]).order(:id).to_a
                         .detect { |w| w.parent.nil? && !owned.include?(w.id) && !claimed.include?(w.id) }
    end
    claimed << found.id if found
    created[k] = found ? found.id : :pending
    under = pk.nil? ? "the project" : (parent_id.is_a?(Integer) ? "##{parent_id} #{pk}" : "#{pk} (made in this run)")
    steps << [k, t, found, "#{found ? "take ##{found.id}" : 'make'}  #{k}  under #{under}  #{t['subject'][0, 70]}"]
  end
  to_make = steps.count { |s| s[2].nil? }
  make_types = rel_count_by(steps.select { |s| s[2].nil? }) { |s| s[1]["type"] }
  make_split = make_types.map { |ty, n| ty + " " + n.to_s }.join(", ")
  rel_say "#{steps.size} keys with no ticket: #{steps.size - to_make} found by subject under their parent, " \
      "#{to_make} to make (#{make_split})"
  rel_list(steps.map { |s| s[3] })
  missing_people = B["create"].flat_map { |k| [by_key[k]["assignee"], by_key[k]["responsible"]] }.compact.uniq
                              .reject { |n| find_user.call(n) }
  rel_say "  people with no active account (left empty): #{missing_people.join(', ')}" if missing_people.any?

  # A New plan ticket under the wrong parent goes under the plan's (what op-check.rb APPLY did); a started one
  # is listed. A parent made in this run is known only after the create step.
  moves, held = [], []
  existing = WorkPackage.where(id: tickets.map { |t| ids[t["key"]] }.compact).to_a
  wp_by_id = {}
  existing.each { |w| wp_by_id[w.id] = w }
  tickets.each do |t|
    id = ids[t["key"]]
    next unless id && wp_by_id[id]
    w = wp_by_id[id]
    want = t["parent"] ? resolve.call(t["parent"]) : nil
    now = w.parent_id
    next if want == now
    line = "##{id} #{t['key']}: under ##{now || '-'}, plan says #{t['parent'] || 'top level'}" +
           (want.is_a?(Integer) ? " (##{want})" : (want == :pending ? " (made in this run)" : ""))
    if w.status_id == NEW_ID
      moves << [id, t["parent"], line]
    else
      held << "#{line} - #{w.status.name}, left"
    end
  end
  rel_say "parents: #{moves.size} New tickets to move under the plan's parent, #{held.size} started ones left where they are"
  rel_list(moves.map { |m| "move #{m[2]}" } + held)

  if APPLY
    started = Time.now
    made = 0
    rel_quietly do
      WorkPackage.transaction do
        steps.each do |k, t, found, _|
          if found
            created[k] = found.id
            next
          end
          parent_id = t["parent"] ? resolve.call(t["parent"]) : nil
          abort("#{k}: parent #{t['parent']} was not made") if t["parent"] && !parent_id.is_a?(Integer)
          wp = WorkPackage.new(project: project, type_id: t["type_id"], subject: t["subject"],
                               description: t["pointer"].gsub("%ID%", "(this ticket)"),
                               priority_id: t["priority_id"], status: Status.default, author: author)
          wp.parent = WorkPackage.find(parent_id) if parent_id
          a = find_user.call(t["assignee"])
          r = find_user.call(t["responsible"])
          wp.assigned_to = a if a
          wp.responsible = r if r
          wp.send("#{version_col}=", t["version"]) if t["version"] && t["set_version"]
          if t["sequence"] && B["field"]
            wp.custom_field_values = { B["field"].sub("customField", "").to_i => t["sequence"] }
          end
          wp.save!
          WorkPackage.where(id: wp.id).update_all(description: t["pointer"].gsub("%ID%", wp.id.to_s))
          created[k] = wp.id
          made += 1
          rel_say "  made ##{wp.id}  #{k}" if made <= 20 || (made % 100).zero?
        end
        moves.each do |id, pk, _|
          w = WorkPackage.find(id)
          pid = pk ? resolve.call(pk) : nil
          w.parent = pid ? WorkPackage.find(pid) : nil
          w.save!
        end
      end
    end
    out = {}
    B["create"].each { |k| out[k] = created[k] if created[k].is_a?(Integer) }
    File.write(CREATED_OUT, JSON.pretty_generate(out))
    rel_say "done: #{made} made, #{out.size - made} taken, #{moves.size} moved in #{(Time.now - started).round(1)}s; " \
        "#{out.size} new ids -> #{CREATED_OUT} (merge into pms-map.json with tools/op-created-merge.py)"
    results << "create: #{made} made, #{out.size - made} taken, #{moves.size} re-parented"
  else
    results << "create: #{to_make} to make, #{steps.size - to_make} to take, #{moves.size} to re-parent"
  end
  rel_phase("guard (with the new ids)")
  merged = ids.dup
  created.each { |k, v| merged[k] = v if v.is_a?(Integer) }
  guard.call(merged, "after create")
  rel_say "ok: #{merged.size} keys, one id each"
end

all_ids = ids.dup
created.each { |k, v| all_ids[k] = v if v.is_a?(Integer) }
id_to_key = all_ids.invert
pending = lambda { |k| !all_ids.key?(k) }
load_wps = lambda do
  h = {}
  WorkPackage.where(id: all_ids.values).includes(:status).to_a.each { |w| h[w.id] = w }
  h
end

# ------------------------------------------------------------------------------------------------------- priority
if rel_run?("priority")
  rel_phase("priority")
  cf_id = B["field"].sub("customField", "").to_i
  field = CustomField.find_by(id: cf_id) or abort("custom field #{cf_id} (#{B['field']}) not found")
  want = {}
  later = 0
  tickets.each do |t|
    next unless t["sequence"]
    if pending.call(t["key"])
      later += 1
    else
      want[all_ids[t["key"]]] = t["sequence"]
    end
  end
  held = CustomValue.where(customized_type: "WorkPackage", customized_id: want.keys, custom_field_id: cf_id)
                    .pluck(:customized_id, :value).to_h
  renumber = want.select { |i, n| held.key?(i) && held[i].to_s != n.to_s }
  add = want.reject { |i, _| held.key?(i) }
  rel_say "field '#{field.name}' (##{cf_id}): #{renumber.size} to renumber, #{add.size} to set for the first time, " \
      "#{want.size - renumber.size - add.size} already right" + (later > 0 ? ", #{later} set when they are made" : "")
  rel_list(renumber.map { |i, n| "##{i} #{id_to_key[i]}: #{held[i]} -> #{n}" } +
            add.map { |i, n| "##{i} #{id_to_key[i]}: (none) -> #{n}" })
  if APPLY
    WorkPackage.transaction do
      renumber.group_by { |_, n| n }.each do |n, list|
        CustomValue.where(customized_type: "WorkPackage", customized_id: list.map(&:first), custom_field_id: cf_id)
                   .update_all(value: n.to_s)
      end
      add.each do |i, n|
        CustomValue.create!(customized_type: "WorkPackage", customized_id: i, custom_field_id: cf_id, value: n.to_s)
      end
    end
    rel_say "done: #{renumber.size + add.size} numbered"
  end
  results << "priority: #{renumber.size} renumbered, #{add.size} set"
end

# --------------------------------------------------------------------------------------------------------- assign
if rel_run?("assign")
  rel_phase("assign")
  wps = load_wps.call
  names = tickets.flat_map { |t| [t["assignee"], t["responsible"]] }.compact.uniq
  nobody = names.reject { |n| find_user.call(n) }
  versions = Version.where(id: B["versions"].values.compact).pluck(:id, :name).to_h
  lost = B["versions"].values.compact - versions.keys
  rel_say "no active OpenProject user (that field left as it is): #{nobody.join(', ')}" if nobody.any?
  rel_say "week versions not found (left as is): #{lost.join(', ')}" if lost.any?
  noted = Journal.where(journable_type: "WorkPackage", journable_id: wps.keys)
                 .where("notes LIKE ?", "%#{ASSIGN_MARKER}%").pluck(:journable_id).to_set
  change, notes, moves = {}, [], Hash.new(0)
  tickets.each do |t|
    id = all_ids[t["key"]]
    w = id && wps[id]
    next unless w
    a = find_user.call(t["assignee"])
    r = find_user.call(t["responsible"])
    v = t["set_version"] && t["version"] && versions.key?(t["version"]) ? t["version"] : nil
    want = {}
    want[:assigned_to_id] = a.id if a && w.assigned_to_id != a.id
    want[:responsible_id] = r.id if r && w.responsible_id != r.id
    want[version_col] = v if v && w.send(version_col) != v
    next if want.empty?
    if w.status_id == NEW_ID
      change[id] = want
      moves["#{w.assigned_to ? w.assigned_to.name : '(none)'} -> #{a.name}"] += 1 if want[:assigned_to_id]
    elsif ENV["ASSIGN_COMMENT"] != "0" && !noted.include?(id) && !w.status.is_closed
      text = "**#{ASSIGN_MARKER}:** this ticket is now planned for **#{a ? a.name : t['assignee']}**" +
             (v ? " in **#{versions[v]}**" : "") + ", accountable **#{r ? r.name : t['responsible']}**. It is " \
             "already #{w.status.name}, so its assignee was not changed; agree the handover with #{author.name} " \
             "if it should move."
      notes << [id, t["key"], w.status.name, text]
    end
  end
  n_of = lambda { |k| change.values.count { |x| x.key?(k) } }
  rel_say "New tickets to change: #{change.size} (assignee #{n_of.call(:assigned_to_id)}, accountable " \
      "#{n_of.call(:responsible_id)}, week #{n_of.call(version_col)}); started tickets that get a comment: #{notes.size}" +
      (ENV["ASSIGN_COMMENT"] == "0" ? " (ASSIGN_COMMENT=0: none)" : "") + "; #{noted.size} already have this release's"
  rel_list(moves.sort_by { |_, n| -n }.map { |m, n| "#{n.to_s.rjust(4)}  #{m}" } +
            notes.map { |id, k, s, _| "comment ##{id} #{k} (#{s})" })
  if APPLY
    now = Time.now
    rel_quietly do
      WorkPackage.transaction do
        change.each { |id, want| WorkPackage.where(id: id).update_all(want.merge(updated_at: now)) }
        notes.each do |id, _, _, text|
          w = WorkPackage.find(id)
          w.add_journal(author, text)
          w.save!(validate: false)
        end
      end
    end
    rel_say "done: #{change.size} tickets changed, #{notes.size} comments"
  end
  results << "assign: #{change.size} changed, #{notes.size} commented"
end

# ---------------------------------------------------------------------------------------------------------- links
if rel_run?("links")
  rel_phase("links")
  after = Hash.new { |h, k| h[k] = [] }
  B["edges"].each { |a, b| after[a] << b }
  memo = {}
  reach = lambda do |start|
    memo[start] ||= begin
      seen, stack = Set.new, after[start].dup
      until stack.empty?
        n = stack.pop
        next if seen.include?(n)
        seen << n
        stack.concat(after[n])
      end
      seen
    end
  end
  task_ids = B["tasks"].map { |k| all_ids[k] }.compact
  direct = Relation.where(from_id: task_ids, to_id: task_ids, follows: 1, hierarchy: 0, relates: 0,
                          duplicates: 0, blocks: 0, includes: 0, requires: 0).to_a
  # compared in keys, not ids: a chain through a ticket made in this run still counts in a dry run
  obsolete = direct.select { |r| !reach.call(id_to_key[r.from_id]).include?(id_to_key[r.to_id]) }
  have = direct.map { |r| [r.from_id, r.to_id] }.to_set
  wanted = B["links"].uniq
  waiting = wanted.count { |a, b| pending.call(a) || pending.call(b) }
  todo = wanted.reject { |a, b| pending.call(a) || pending.call(b) }
               .map { |a, b| [all_ids[a], all_ids[b]] }.reject { |pair| have.include?(pair) }
  todo = todo.first(LINK_LIMIT) if LINK_LIMIT
  rel_say "#{direct.size} direct follows links between plan tasks now; #{obsolete.size} the plan no longer orders " \
      "(removed first); #{wanted.size} the plan wants: #{wanted.size - waiting - todo.size} there, #{todo.size} to add" +
      (waiting > 0 ? ", #{waiting} wait for tickets made in this run" : "") + (LINK_LIMIT ? " (LIMIT=#{LINK_LIMIT})" : "")
  rel_list(obsolete.map { |r| "remove ##{r.from_id} #{id_to_key[r.from_id]} follows ##{r.to_id} #{id_to_key[r.to_id]}" } +
            todo.map { |a, b| "add    ##{a} #{id_to_key[a]} follows ##{b} #{id_to_key[b]}" })
  if APPLY
    started = Time.now
    rows_before = Relation.count
    made = twice = 0
    rel_quietly do
      WorkPackage.transaction do
        obsolete.each(&:destroy)
        todo.each do |from_id, to_id|
          r = Relation.new(from_id: from_id, to_id: to_id)
          r.relation_type = Relation::TYPE_FOLLOWS
          begin
            # a savepoint, so a duplicate does not abort the phase's transaction (PostgreSQL)
            Relation.transaction(requires_new: true) { r.save!(validate: false) }
            made += 1
          rescue ActiveRecord::RecordNotUnique
            twice += 1
          end
          rel_say "  #{made + twice}/#{todo.size} links (#{(Time.now - started).round}s)" if ((made + twice) % 100).zero?
        end
      end
    end
    rel_say "done: #{obsolete.size} removed, #{made} added, #{twice} already there, in #{(Time.now - started).round}s; " \
        "relations table #{rows_before} -> #{Relation.count} rows"
    results << "links: #{obsolete.size} removed, #{made} added"
  else
    results << "links: #{obsolete.size} to remove, #{todo.size} to add"
  end
end

# --------------------------------------------------------------------------------------------------------- retire
if rel_run?("retire")
  rel_phase("retire")
  list = B["retire"]
  found = {}
  WorkPackage.where(id: list.map { |e| e["id"] }).includes(:status).to_a.each { |w| found[w.id] = w }
  act, done_already, started_left, gone = [], [], [], []
  list.each do |e|
    w = found[e["id"]]
    target = e["action"] == "defer" ? status_hold : status_rejected
    if w.nil?
      gone << "##{e['id']} #{e['key']}: not in OpenProject any more"
    elsif w.project_id != PROJECT_ID
      gone << "##{e['id']} #{e['key']}: in another project, left"
    elsif w.status_id == target.id
      done_already << e
    elsif w.status_id != NEW_ID
      started_left << "##{e['id']} #{e['key']}: #{w.status.name}, not New - left alone"
    else
      act << [e, target]
    end
  end
  act_types = rel_count_by(act) { |x| x[0]["action"] }
  act_split = act_types.map { |k, n| k + " " + n.to_s }.join(", ")
  rel_say "#{list.size} tickets leaving the plan: #{act.size} to move (#{act_split}), " \
      "#{done_already.size} already moved, #{started_left.size} started (left), #{gone.size} gone"
  rel_list(act.map { |e, t| "#{e['action'].ljust(5)} ##{e['id']} #{e['key']} -> #{t.name}" } + started_left + gone)
  rel_say "unexplained (never touched): #{B['unexplained'].size}"
  rel_list(B["unexplained"].map { |u| "?? ##{u['id']} #{u['key']}: #{u['why']}" })
  if APPLY
    rel_quietly do
      WorkPackage.transaction do
        act.each do |e, target|
          w = WorkPackage.find(e["id"])
          w.status_id = target.id
          if e["action"] == "defer"
            w.assigned_to = nil
            w.send("#{version_col}=", nil)
          end
          w.add_journal(author, e["note"])
          w.save!(validate: false)
        end
      end
    end
    rel_say "done: #{act.size} moved"
  end
  results << "retire: #{act.size} #{APPLY ? 'moved' : 'to move'}, #{B['unexplained'].size} unexplained listed"
end

# --------------------------------------------------------------------------------------------------- descriptions
norm = lambda do |text|
  text.to_s.gsub("\r\n", "\n").split("\n").reject { |l| l.start_with?(RELEASE_PREFIX) }.join("\n").strip
end
if rel_run?("descriptions")
  rel_phase("descriptions")
  wps = load_wps.call
  commented = Journal.where(journable_type: "WorkPackage", journable_id: wps.keys)
                     .where("notes LIKE ?", "%#{COMMENT_MARKER}%").pluck(:journable_id).to_set
  rewrite, comment, retitle, kept_titles = [], [], [], []
  same = already_pointer = already_commented = closed = 0
  ordered = tickets.sort_by { |t| [t["sequence"] || 999_999, t["key"]] }
  ordered.each do |t|
    id = all_ids[t["key"]]
    w = id && wps[id]
    next unless w
    want = t["pointer"].gsub("%ID%", id.to_s)
    if w.status_id == NEW_ID
      if norm.call(w.description) == norm.call(want)
        same += 1
      else
        rewrite << [id, t["key"], want, w.description.to_s.size]
      end
    elsif w.description.to_s.include?(POINTER_PREFIX)
      already_pointer += 1
    elsif commented.include?(id)
      already_commented += 1
    elsif w.status.is_closed
      closed += 1
    else
      comment << [id, t["key"], w.status.name, B["comment"].gsub("%ID%", id.to_s).gsub("%KEY%", t["key"])]
    end
    if w.subject != t["subject"]
      if w.status_id == NEW_ID || ENV["RETITLE"] == "all"
        retitle << [id, t["key"], w.subject, t["subject"]]
      else
        kept_titles << "##{id} #{t['key']} (#{w.status.name}): keeps '#{w.subject[0, 60]}', plan says '#{t['subject'][0, 60]}'"
      end
    end
  end
  rw = BATCH ? rewrite.first(BATCH) : rewrite
  cm = BATCH ? comment.first(BATCH) : comment
  rel_say "New tickets: #{rewrite.size} to rewrite to the pointer, #{same} already the pointer" +
      (BATCH ? " (BATCH=#{BATCH}: #{rw.size} this run, #{rewrite.size - rw.size} left for the next)" : "")
  rel_say "started tickets (text kept): #{comment.size} to get the one comment, #{already_commented} already have it, " \
      "#{already_pointer} already carry a pointer, #{closed} closed (no comment)" +
      (BATCH ? " (BATCH=#{BATCH}: #{cm.size} this run)" : "")
  rel_say "titles: #{retitle.size} to retitle, #{kept_titles.size} on started tickets kept (RETITLE=all changes them too)"
  rel_list(rw.map { |i, k, _, was| "rewrite ##{i} #{k} (#{was} -> pointer)" } +
            cm.map { |i, k, s, _| "comment ##{i} #{k} (#{s})" } +
            retitle.map { |i, k, was, now| "retitle ##{i} #{k}: '#{was[0, 50]}' -> '#{now[0, 50]}'" } + kept_titles)
  sample = rw.first
  if sample
    rel_say "  e.g. ##{sample[0]} becomes:"
    sample[2].split("\n").each { |l| rel_say "    | #{l}" }
  end
  sample = cm.first
  rel_say "  e.g. comment on ##{sample[0]}: #{sample[3]}" if sample
  if APPLY
    now = Time.now
    rel_quietly do
      WorkPackage.transaction do
        rw.each { |i, _, text, _| WorkPackage.where(id: i).update_all(description: text, updated_at: now) }
        retitle.each { |i, _, _, s| WorkPackage.where(id: i, project_id: PROJECT_ID).update_all(subject: s, updated_at: now) }
        cm.each do |i, _, _, text|
          w = WorkPackage.find(i)
          w.add_journal(author, text)
          w.save!(validate: false)
        end
      end
    end
    rel_say "done: #{rw.size} rewritten, #{cm.size} commented, #{retitle.size} retitled"
  end
  results << "descriptions: #{rw.size} rewritten, #{cm.size} commented, #{retitle.size} retitled" +
             (rewrite.size > rw.size || comment.size > cm.size ? "; #{rewrite.size - rw.size + comment.size - cm.size} left for the next BATCH" : "")
end

# --------------------------------------------------------------------------------------------------------- health
if rel_run?("health")
  rel_phase("health (read-only)")
  all = WorkPackage.where(project_id: PROJECT_ID).includes(:status, :type).to_a
  by_id = {}
  all.each { |w| by_id[w.id] = w }
  open_wps = all.reject { |w| w.status.is_closed }
  rel_say "project ##{PROJECT_ID}: #{all.size} tickets (#{open_wps.size} open); plan #{tickets.size}, " \
      "#{tickets.count { |t| all_ids.key?(t['key']) }} with an id; #{left_ids.size} leaving the plan"

  groups = Hash.new { |h, k| h[k] = [] }
  open_wps.each { |w| groups[[w.parent_id, w.subject.to_s.strip.downcase]] << w }
  dups = groups.select { |_, ws| ws.size > 1 }
  rel_say "1. duplicates (open, same subject, same parent): #{dups.size} groups"
  rel_list(dups.map { |(par, _), ws| "under ##{par || '-'}: " + ws.sort_by(&:id).map { |w| "##{w.id} #{id_to_key[w.id] || 'no key'}" }.join(", ") })

  plan_rows = tickets.select { |t| all_ids.key?(t["key"]) }
  missing = plan_rows.reject { |t| by_id.key?(all_ids[t["key"]]) }
  wrong_type = plan_rows.select { |t| (w = by_id[all_ids[t["key"]]]) && w.type_id != t["type_id"] }
  wrong_parent = plan_rows.select do |t|
    w = by_id[all_ids[t["key"]]]
    w && w.parent_id != (t["parent"] ? all_ids[t["parent"]] : nil)
  end
  rel_say "2. plan tickets missing: #{missing.size}; wrong type: #{wrong_type.size}; under the wrong parent: #{wrong_parent.size}"
  rel_list(missing.map { |t| "missing ##{all_ids[t['key']]} #{t['key']}" } +
            wrong_type.map { |t| "type ##{all_ids[t['key']]} #{t['key']}: #{by_id[all_ids[t['key']]].type.name}, plan #{t['type']}" } +
            wrong_parent.map { |t| w = by_id[all_ids[t["key"]]]; "parent ##{w.id} #{t['key']} (#{w.status.name}): under ##{w.parent_id || '-'}, plan #{t['parent'] || 'top level'}" })

  known = all_ids.values.to_set
  unknown = all.reject { |w| known.include?(w.id) || left_ids.include?(w.id) }
  rel_say "3. tickets the plan does not know: #{unknown.size} (#{unknown.count { |w| !w.status.is_closed }} open)"
  rel_list(unknown.sort_by(&:id).map { |w| "##{w.id} #{w.type.name} (#{w.status.name}) #{w.subject.to_s[0, 70]}" })

  project_ids = all.map(&:id)
  rejected = all.select { |w| w.status_id == status_rejected.id }.map(&:id)
  direct = Relation.where(follows: 1, hierarchy: 0, relates: 0, duplicates: 0, blocks: 0, includes: 0, requires: 0)
  bad = direct.where(from_id: rejected).or(direct.where(to_id: rejected)).to_a
  outside = direct.where(from_id: project_ids).where.not(to_id: project_ids).count +
            direct.where(to_id: project_ids).where.not(from_id: project_ids).count
  rel_say "4. follows links touching a Rejected ticket: #{bad.size}; links leaving the project: #{outside}"
  rel_list(bad.map { |r| "##{r.from_id} follows ##{r.to_id}" })

  new_plan = plan_rows.map { |t| [t, by_id[all_ids[t["key"]]]] }.select { |_, w| w && w.status_id == NEW_ID }
  not_pointer = new_plan.count { |t, w| norm.call(w.description) != norm.call(t["pointer"].gsub("%ID%", w.id.to_s)) }
  rel_say "5. pointers: #{new_plan.size - not_pointer} of #{new_plan.size} New plan tickets carry their pointer" +
      (not_pointer > 0 ? " (#{not_pointer} still to rewrite: run ONLY=descriptions again)" : "")
  results << "health: #{dups.size} duplicate groups, #{missing.size} missing, #{wrong_parent.size} wrong parent, " \
             "#{unknown.size} unknown, #{bad.size} links to Rejected, #{not_pointer} New without pointer"
end

rel_say ""
rel_say "== summary #{APPLY ? '(APPLIED)' : '(dry run: nothing written; APPLY=1 applies)'}"
results.each { |r| rel_say "  #{r}" }
