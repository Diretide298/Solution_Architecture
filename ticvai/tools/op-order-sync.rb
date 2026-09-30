# Bring the tickets already in OpenProject in line with the plan's build order (OpenProject 10, container "openproject").
#
# Two things drift when the plan changes, and nothing else fixes them:
#   1. Priority_No. (the build order as a number) is set when a ticket is made and never again. Every ticket in
#      op-order.json gets its number now, started and closed ones too: it is an order, not content.
#   2. "follows" links are only ever added. A direct link between two plan tasks whose order the plan no longer
#      has, directly or through a chain, is removed. Links that touch a ticket outside the plan's tasks (a bug, a
#      retired ticket, a sub-task) are never touched. Every removal is listed in the dry run first.
#
# Writes without journals or mail: Priority_No. through update_all on custom_values; a link through
# Relation#destroy, whose callbacks keep OpenProject 10's derived rows (typed_dag) consistent.
#
# Make op-order.json here with tools/op-order-sync.py. Backup first (see OPENPROJECT-PUSH.md), then:
#   docker cp tools/op-order-sync.rb openproject:/tmp/ && docker cp handoff/service-docs/op-order.json openproject:/tmp/
#   dry run:  docker exec openproject bash -c 'cd /app && bundle exec rails runner /tmp/op-order-sync.rb /tmp/op-order.json'
#   apply:    docker exec -e APPLY=1 openproject bash -c 'cd /app && bundle exec rails runner /tmp/op-order-sync.rb /tmp/op-order.json'
#   PRUNE=0 renumbers only and leaves every link in place.

PROJECT_ID = 153
path = ARGV[0] or abort("usage: rails runner op-order-sync.rb op-order.json")
plan = JSON.parse(File.read(path))
apply = ENV["APPLY"] == "1"
prune = ENV["PRUNE"] != "0"

cf_id = plan["field"].sub("customField", "").to_i
field = CustomField.find_by(id: cf_id) or abort("custom field #{cf_id} not found")
priority = plan["priority"].transform_keys(&:to_i)
wps = WorkPackage.where(id: priority.keys, project_id: PROJECT_ID).pluck(:id).to_set
gone = priority.keys.reject { |i| wps.include?(i) }
puts "OpenProject #{OpenProject::VERSION}: field '#{field.name}' (##{cf_id}); #{priority.size} tickets in the file, " \
     "#{gone.size} not in project #{PROJECT_ID} (skipped)"

held = CustomValue.where(customized_type: "WorkPackage", customized_id: wps.to_a, custom_field_id: cf_id)
                  .pluck(:customized_id, :value).to_h
renumber = priority.select { |i, n| wps.include?(i) && held.key?(i) && held[i].to_s != n.to_s }
add = priority.select { |i, _| wps.include?(i) && !held.key?(i) }
puts "Priority_No.: #{renumber.size} to renumber, #{add.size} to set for the first time, " \
     "#{priority.size - renumber.size - add.size - gone.size} already right"

# what the plan orders: a pair [a, b] is kept when b can be reached from a through the plan's waits
after = Hash.new { |h, k| h[k] = [] }
plan["edges"].each { |a, b| after[a] << b }
tasks = plan["tasks"].to_set
reach = lambda do |start|
  seen, stack = Set.new, after[start].dup
  until stack.empty?
    n = stack.pop
    next if seen.include?(n)
    seen << n
    stack.concat(after[n])
  end
  seen
end
direct = Relation.where(from_id: tasks.to_a, to_id: tasks.to_a, follows: 1, hierarchy: 0, relates: 0,
                        duplicates: 0, blocks: 0, includes: 0, requires: 0)
cache = {}
obsolete = direct.select { |r| !(cache[r.from_id] ||= reach.call(r.from_id)).include?(r.to_id) }
puts "links: #{direct.count} direct follows links between plan tasks; #{obsolete.size} no longer in the plan" +
     (prune ? "" : " (PRUNE=0: kept)")
obsolete.first(40).each { |r| puts "  remove: ##{r.from_id} follows ##{r.to_id}" }
puts "  ... and #{obsolete.size - 40} more" if obsolete.size > 40
exit unless apply

started = Time.now
WorkPackage.transaction do
  renumber.group_by { |_, n| n }.each do |n, list|
    CustomValue.where(customized_type: "WorkPackage", customized_id: list.map(&:first), custom_field_id: cf_id)
               .update_all(value: n.to_s)
  end
  add.each do |i, n|
    CustomValue.create!(customized_type: "WorkPackage", customized_id: i, custom_field_id: cf_id, value: n.to_s)
  end
end
removed = 0
if prune
  obsolete.each do |r|
    r.destroy
    removed += 1
  end
end
puts "done: #{renumber.size + add.size} numbered, #{removed} links removed in #{(Time.now - started).round(1)}s. " \
     "Then run op-bulk-links.rb with a fresh op-links.json to add the plan's new links."
