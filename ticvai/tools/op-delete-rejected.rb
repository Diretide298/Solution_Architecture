# Delete the tickets tools/op-retire.py closed as Rejected because another ticket carries their work (duplicates
# under a renamed key, merged screens), with their sub-tasks. Written on Chinmay's request, 30 September 2026.
# OpenProject 10, container "openproject". Deleting cannot be undone: back up the database first.
#
# The list comes from rejected.json (id -> plan key), so a ticket a person rejected by hand is never touched. A
# ticket is deleted only if it is still Rejected, has no time logged, and every sub-task under it is in the list
# too; anything else is listed and kept. Dry run unless APPLY=1.
#
#   dry run:  docker exec openproject bash -c 'cd /app && bundle exec rails runner /tmp/op-delete-rejected.rb /tmp/rejected.json'
#   apply:    docker exec -e APPLY=1 openproject bash -c 'cd /app && bundle exec rails runner /tmp/op-delete-rejected.rb /tmp/rejected.json'

path = ARGV[0] or abort("usage: rails runner op-delete-rejected.rb rejected.json")
plan = JSON.parse(File.read(path))
apply = ENV["APPLY"] == "1"
listed = plan["tickets"].transform_keys(&:to_i)

wps = WorkPackage.where(id: listed.keys, project_id: plan["project"]).includes(:status).to_a
gone = listed.keys - wps.map(&:id)
keep, del = {}, []
wps.each do |wp|
  extra = wp.descendants.pluck(:id) - listed.keys
  if wp.status.name != "Rejected"
    keep[wp] = "status is #{wp.status.name}"
  elsif TimeEntry.where(work_package_id: wp.id).exists?
    keep[wp] = "time is logged on it"
  elsif extra.any?
    keep[wp] = "sub-tasks not in the list: #{extra.first(5).map { |i| "##{i}" }.join(', ')}"
  else
    del << wp
  end
end
kept_ids = keep.keys.map(&:id)
del.reject! { |wp| (wp.descendants.pluck(:id) & kept_ids).any? && (keep[wp] = "a sub-task under it is kept") }

puts "OpenProject #{OpenProject::VERSION}: #{listed.size} in the file, #{gone.size} already gone, " \
     "#{del.size} to delete, #{keep.size} kept"
del.select { |w| w.parent_id.nil? || !listed.key?(w.parent_id) }.each do |w|
  puts "  delete ##{w.id} #{listed[w.id]}: #{w.subject[0, 70]} (+#{w.descendants.count} sub-tasks)"
end
keep.each { |w, why| puts "  keep   ##{w.id} #{listed[w.id]}: #{why}" }
exit unless apply

started = Time.now
done = 0
del.sort_by { |w| -w.ancestors.count }.each do |wp|
  next unless WorkPackage.exists?(wp.id)
  WorkPackage.find(wp.id).destroy
  done += 1
end
puts "done: #{done} deleted in #{(Time.now - started).round(1)}s"
