# Make the work packages push-openproject.py --export listed, on the server (OpenProject 10, container "openproject").
#
# Through the API each new sub-task under a big migration task took OpenProject longer than Cloudflare's
# 100 seconds (28 September): the request failed while the ticket was made anyway, and a retry made copies.
# Here there is no proxy in the way. Notifications are off, so assignees get no mail per ticket.
#
# Safe to run twice: a work package with the same subject under the same parent is found, not made again.
# Prints {key: id} and writes it to /tmp/op-created.json; add those to pms-map.json (tools/op-created-merge.py).
#
#   docker cp /tmp/op-create.rb openproject:/tmp/ && docker cp /tmp/op-create.json openproject:/tmp/
#   dry run:  docker exec openproject bash -c 'cd /app && bundle exec rails runner /tmp/op-create.rb /tmp/op-create.json'
#   apply:    docker exec -e APPLY=1 openproject bash -c 'cd /app && bundle exec rails runner /tmp/op-create.rb /tmp/op-create.json'
#   then:     docker cp openproject:/tmp/op-created.json /tmp/

PROJECT_ID = 153
path = ARGV[0] or abort("usage: rails runner op-create.rb op-create.json")
items = JSON.parse(File.read(path))
apply = ENV["APPLY"] == "1"

project = Project.find(PROJECT_ID)
users = User.active.to_a.map { |u| [u.name, u] }.to_h
# Everything these scripts write is authored by Chinmay Parab, never by whichever account happens to be the
# instance admin: on 30 September tickets made with the old "admin, else the first admin" fallback showed up
# under Sameer Shinde, who is not on the project. AUTHOR (a login or an email) overrides; nothing falls back.
author = (ENV["AUTHOR"] && (User.find_by(login: ENV["AUTHOR"]) || User.find_by(mail: ENV["AUTHOR"]))) ||
         User.active.detect { |u| u.name == "Chinmay Parab" }
abort("author not found: no active user named Chinmay Parab; run with AUTHOR=<his login>") unless author
version_col = WorkPackage.column_names.include?("version_id") ? :version_id : :fixed_version_id

plan = items.map do |e|
  parent = WorkPackage.find_by(id: e["parent_id"])
  abort("#{e['key']}: parent ##{e['parent_id']} not found") if e["parent_id"] && !parent
  abort("#{e['key']}: parent ##{parent.id} is not in project #{PROJECT_ID}") if parent && parent.project_id != PROJECT_ID
  found = parent && parent.children.where(subject: e["subject"]).order(:id).first
  [e, parent, found]
end
missing_users = items.flat_map { |e| [e["assignee"], e["responsible"]] }.compact.uniq - users.keys
puts "OpenProject #{OpenProject::VERSION}: #{items.size} in the file, #{plan.count { |_, _, f| f }} already there, " \
     "#{plan.count { |_, _, f| !f }} to make"
puts "users not found (left empty): #{missing_users.join(', ')}" if missing_users.any?
plan.each { |e, parent, f| puts "  #{f ? "there ##{f.id}" : 'make'}  #{e['key']}  under ##{parent&.id}" }
exit unless apply

quiet = defined?(Journal::NotificationConfiguration) ? Journal::NotificationConfiguration.method(:with) : nil
created = {}
started = Time.now
plan.each do |e, parent, found|
  if found
    created[e["key"]] = found.id
    next
  end
  wp = WorkPackage.new(project: project, type_id: e["type_id"], subject: e["subject"], description: e["description"],
                       priority_id: e["priority_id"], status: Status.default, author: author)
  wp.parent = parent if parent
  wp.assigned_to = users[e["assignee"]] if e["assignee"]
  wp.responsible = users[e["responsible"]] if e["responsible"]
  wp.send("#{version_col}=", e["version_id"]) if e["version_id"]
  if e["sequence"] && e["priority_no_field"]
    wp.custom_field_values = { e["priority_no_field"].sub("customField", "").to_i => e["sequence"] }
  end
  save = -> { wp.save! }
  quiet ? quiet.call(false, &save) : save.call
  created[e["key"]] = wp.id
  puts "  made ##{wp.id}  #{e['key']}"
end
File.write("/tmp/op-created.json", JSON.pretty_generate(created))
puts "done: #{created.size} recorded (#{(Time.now - started).round(1)}s) -> /tmp/op-created.json"
