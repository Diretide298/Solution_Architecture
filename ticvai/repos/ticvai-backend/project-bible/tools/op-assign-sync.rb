# Bring each ticket's assignee, accountable and Block A week in line with the plan (OpenProject 10, container
# "openproject"). Make op-assign.json here with tools/op-assign-sync.py.
#
# Only a ticket nobody has started (status New) is changed; the people on a started ticket are a conversation, so
# it gets a comment naming who the plan now gives it to, and keeps its assignee. A person the plan names who has
# no active OpenProject account (e.g. "Second AI engineer") is listed and that field left as it is: a ticket is
# never unassigned by this script. Written with notifications off, so nobody is mailed.
#
#   docker cp op-assign-sync.rb openproject:/tmp/ && docker cp op-assign.json openproject:/tmp/
#   dry run:  docker exec openproject bash -c 'cd /app && bundle exec rails runner /tmp/op-assign-sync.rb /tmp/op-assign.json'
#   apply:    docker exec -e APPLY=1 openproject bash -c 'cd /app && bundle exec rails runner /tmp/op-assign-sync.rb /tmp/op-assign.json'
#   COMMENT=0 skips the comments on started tickets.

path = ARGV[0] or abort("usage: rails runner op-assign-sync.rb op-assign.json")
plan = JSON.parse(File.read(path))
apply = ENV["APPLY"] == "1"
comment = ENV["COMMENT"] != "0"
tickets = plan["tickets"].transform_keys(&:to_i)

users = User.active.to_a.map { |u| [u.name, u] }.to_h
unknown = plan["people"].reject { |n| users.key?(n) }
author = (ENV["AUTHOR"] && (User.find_by(login: ENV["AUTHOR"]) || User.find_by(mail: ENV["AUTHOR"]))) ||
         User.active.detect { |u| u.name == "Chinmay Parab" }
abort("author not found: no active user named Chinmay Parab; run with AUTHOR=<his login>") unless author
version_col = WorkPackage.column_names.include?("version_id") ? :version_id : :fixed_version_id
versions = Version.where(id: tickets.values.map { |t| t["version"] }.compact.uniq).pluck(:id, :name).to_h

wps = WorkPackage.where(id: tickets.keys, project_id: plan["project"]).includes(:status).to_a
puts "OpenProject #{OpenProject::VERSION}: #{tickets.size} tickets in the file, #{wps.size} found in project #{plan['project']}"
puts "no active OpenProject user (left as is): #{unknown.join(', ')}" if unknown.any?

change, notes = {}, {}
moves = Hash.new(0)
wps.each do |wp|
  t = tickets[wp.id]
  want = {}
  a = users[t["assignee"]]&.id
  r = users[t["responsible"]]&.id
  want[:assigned_to_id] = a if a && wp.assigned_to_id != a
  want[:responsible_id] = r if r && wp.responsible_id != r
  want[version_col] = t["version"] if t["setVersion"] && t["version"] && wp.send(version_col) != t["version"]
  next if want.empty?
  if wp.status.name == "New"
    change[wp] = want
    moves["#{wp.assigned_to&.name || '(none)'} -> #{t['assignee']}"] += 1 if want[:assigned_to_id]
  else
    notes[wp] = "**Plan update (30 September):** this ticket is now planned for **#{t['assignee']}**" +
                (t["version"] ? " in **#{versions[t['version']]}**" : "") +
                ", accountable **#{t['responsible']}**. It is already #{wp.status.name}, so its assignee was not " \
                "changed; agree the handover with Chinmay Parab if it should move."
  end
end

count = ->(k) { change.values.count { |w| w.key?(k) } }
puts "New tickets to change: #{change.size} (assignee #{count.(:assigned_to_id)}, accountable " \
     "#{count.(:responsible_id)}, week #{count.(version_col)}); started tickets that get a comment: #{notes.size}"
moves.sort_by { |_, n| -n }.first(25).each { |m, n| puts "  #{n.to_s.rjust(4)}  #{m}" }
notes.keys.first(15).each { |w| puts "  comment ##{w.id} (#{w.status.name}): #{tickets[w.id]['key']} -> #{tickets[w.id]['assignee']}" }
exit unless apply

started = Time.now
WorkPackage.transaction do
  change.each { |wp, want| WorkPackage.where(id: wp.id).update_all(want.merge(updated_at: Time.now)) }
end
if comment && notes.any?
  quiet = defined?(Journal::NotificationConfiguration) ? Journal::NotificationConfiguration.method(:with) : nil
  notes.each do |wp, text|
    wp.add_journal(author, text)
    save = -> { wp.save!(validate: false) }
    quiet ? quiet.call(false, &save) : save.call
  end
end
puts "done: #{change.size} tickets changed, #{comment ? notes.size : 0} comments in #{(Time.now - started).round(1)}s"
