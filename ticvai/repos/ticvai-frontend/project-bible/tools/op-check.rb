# Health check of the TICVAI project in OpenProject (OpenProject 10, container "openproject") against the plan.
# Make op-check.json here with tools/op-check.py.
#
# Read-only by default. It reports:
#   1. duplicates: two or more open tickets with the same subject under the same parent
#   2. plan tickets missing from the project, or of the wrong type
#   3. plan tickets under the wrong parent
#   4. tickets in the project that the plan does not know (made by hand, or by a run that was not recorded)
#   5. follows links that touch a Rejected ticket, and links that go outside the project
#
# APPLY=1 fixes only what is safe to fix without a person: a NEW plan ticket under the wrong parent is moved under
# the plan's parent, and follows links that touch a Rejected ticket are removed. Nothing is ever deleted;
# duplicates and unknown tickets are only listed, for Chinmay to decide. No mail is sent. Back up first.
#
#   dry run:  docker exec openproject bash -c 'cd /app && bundle exec rails runner /tmp/op-check.rb /tmp/op-check.json'
#   apply:    docker exec -e APPLY=1 openproject bash -c 'cd /app && bundle exec rails runner /tmp/op-check.rb /tmp/op-check.json'

path = ARGV[0] or abort("usage: rails runner op-check.rb op-check.json")
plan = JSON.parse(File.read(path))
apply = ENV["APPLY"] == "1"
pid = plan["project"]
want = plan["tickets"].transform_keys(&:to_i)
retired = plan["retired"].to_set

all = WorkPackage.where(project_id: pid).includes(:status, :type).to_a
by_id = all.map { |w| [w.id, w] }.to_h
open_wps = all.reject { |w| w.status.is_closed }
puts "OpenProject #{OpenProject::VERSION}: project #{pid} has #{all.size} tickets (#{open_wps.size} open); " \
     "the plan has #{want.size}, #{retired.size} retired"

def show(list, n = 30)
  list.first(n).each { |l| puts "    #{l}" }
  puts "    ... and #{list.size - n} more" if list.size > n
end

# 1. duplicates
dups = open_wps.group_by { |w| [w.parent_id, w.subject.strip.downcase] }.select { |_, ws| ws.size > 1 }
puts "\n1. Duplicates (same subject, same parent, open): #{dups.size} groups"
show(dups.map { |(par, _), ws|
  ws = ws.sort_by(&:id)
  keys = ws.map { |w| want[w.id] ? want[w.id]["key"] : (retired.include?(w.id) ? "retired" : "not in plan") }
  "under ##{par || '-'}: #{ws.first.subject[0, 60]} -> " + ws.zip(keys).map { |w, k| "##{w.id} (#{w.status.name}, #{k})" }.join(", ")
})

# 2. missing or wrong type
missing = want.keys.reject { |i| by_id.key?(i) }
wrong_type = want.select { |i, t| by_id[i] && by_id[i].type_id != t["type"] }
puts "\n2. Plan tickets missing from the project: #{missing.size}; wrong type: #{wrong_type.size}"
show(missing.map { |i| "missing ##{i} #{want[i]['key']}" })
show(wrong_type.map { |i, t| "##{i} #{t['key']}: type #{by_id[i].type.name}, plan type id #{t['type']}" })

# 3. wrong parent
wrong_parent = want.select { |i, t| by_id[i] && by_id[i].parent_id != t["parent"] }
fixable = wrong_parent.select { |i, t| by_id[i].status.name == "New" && (t["parent"].nil? || by_id.key?(t["parent"])) }
puts "\n3. Plan tickets under the wrong parent: #{wrong_parent.size} (#{fixable.size} New, fixable)"
show(wrong_parent.map { |i, t| "##{i} #{t['key']} (#{by_id[i].status.name}): under ##{by_id[i].parent_id || '-'}, plan says ##{t['parent'] || '-'}" })

# 4. unknown tickets
unknown = all.reject { |w| want.key?(w.id) || retired.include?(w.id) }
puts "\n4. Tickets the plan does not know: #{unknown.size} (#{unknown.count { |w| !w.status.is_closed }} open)"
show(unknown.sort_by(&:id).map { |w| "##{w.id} #{w.type.name} (#{w.status.name}) #{w.subject[0, 70]} under ##{w.parent_id || '-'}" }, 40)

# 5. links
ids = all.map(&:id)
rejected = all.select { |w| w.status.name == "Rejected" }.map(&:id)
direct = Relation.where(follows: 1, hierarchy: 0, relates: 0, duplicates: 0, blocks: 0, includes: 0, requires: 0)
bad_links = direct.where(from_id: rejected).or(direct.where(to_id: rejected)).to_a
outside = direct.where(from_id: ids).where.not(to_id: ids).count + direct.where(to_id: ids).where.not(from_id: ids).count
puts "\n5. Follows links touching a Rejected ticket: #{bad_links.size}; links to tickets outside the project: #{outside}"
show(bad_links.map { |r| "##{r.from_id} follows ##{r.to_id}" })

exit unless apply
puts "\nAPPLY: moving #{fixable.size} New tickets to their plan parent, removing #{bad_links.size} links"
quiet = defined?(Journal::NotificationConfiguration) ? Journal::NotificationConfiguration.method(:with) : nil
fixable.each do |i, t|
  wp = WorkPackage.find(i)
  wp.parent = t["parent"] ? WorkPackage.find(t["parent"]) : nil
  save = -> { wp.save! }
  quiet ? quiet.call(false, &save) : save.call
end
bad_links.each(&:destroy)
puts "done"
