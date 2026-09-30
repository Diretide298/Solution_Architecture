# Put the project's tickets back in Chinmay Parab's name (OpenProject 10, container "openproject").
#
# On 30 September some tickets showed under Sameer Shinde, who is not on the project: op-create.rb and
# op-descriptions.rb used to write as the "admin" login, or else the first admin on the instance. They now
# write as Chinmay Parab only. This script repairs what was already written:
#   - a ticket whose author is not Chinmay Parab and not a member of the project gets Chinmay as its author;
#   - a ticket assigned to, or accountable to, somebody who is not a member of the project gets Chinmay
#     instead, so nothing sits with a person who cannot see it;
#   - the history entries (journals) those people wrote on these tickets are put in Chinmay's name.
# Members of the project keep everything they hold. Nothing is sent: update_all writes no journal and no mail.
#
#   docker cp tools/op-reauthor.rb openproject:/tmp/
#   dry run:  docker exec openproject bash -c 'cd /app && bundle exec rails runner /tmp/op-reauthor.rb'
#   apply:    docker exec -e APPLY=1 openproject bash -c 'cd /app && bundle exec rails runner /tmp/op-reauthor.rb'
#   AUTHOR=<login or email> picks Chinmay's account if his name is spelt differently on the server.

PROJECT_ID = 153
apply = ENV["APPLY"] == "1"

project = Project.find(PROJECT_ID)
me = (ENV["AUTHOR"] && (User.find_by(login: ENV["AUTHOR"]) || User.find_by(mail: ENV["AUTHOR"]))) ||
     User.active.detect { |u| u.name == "Chinmay Parab" }
abort("no active user named Chinmay Parab; run with AUTHOR=<his login>") unless me

members = Member.where(project_id: PROJECT_ID).pluck(:user_id).to_set
members << me.id
outsider = ->(id) { id && !members.include?(id) }

wps = WorkPackage.where(project_id: PROJECT_ID)
fix = { author_id: [], assigned_to_id: [], responsible_id: [] }
who = Hash.new(0)
wps.pluck(:id, :author_id, :assigned_to_id, :responsible_id).each do |id, author, assignee, accountable|
  { author_id: author, assigned_to_id: assignee, responsible_id: accountable }.each do |col, uid|
    next unless outsider.call(uid)
    next if col == :author_id && uid == me.id
    fix[col] << id
    who[[col, uid]] += 1
  end
end
journals = Journal.where(journable_type: "WorkPackage", journable_id: wps.select(:id))
                  .where.not(user_id: members.to_a)

names = User.where(id: who.keys.map(&:last).uniq).map { |u| [u.id, u.name] }.to_h
puts "project ##{PROJECT_ID} #{project.name}: #{wps.count} tickets, #{members.size} members; author to be: #{me.name}"
who.each { |(col, uid), n| puts "  #{col.to_s.sub('_id', '').ljust(12)} #{names[uid] || "user ##{uid}"} (not a member): #{n}" }
history = journals.count
puts "  history entries by non-members: #{history}"
if fix.values.all?(&:empty?) && history.zero?
  puts "nothing to repair"
  exit
end
exit unless apply

WorkPackage.transaction do
  fix.each { |col, ids| WorkPackage.where(id: ids).update_all(col => me.id) if ids.any? }
  journals.update_all(user_id: me.id)
end
puts "done: " + fix.map { |col, ids| "#{col.to_s.sub('_id', '')} #{ids.size}" }.join(", ") +
     ", history #{history} (now #{me.name})"
