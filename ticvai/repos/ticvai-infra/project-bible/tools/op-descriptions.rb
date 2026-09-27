# Write the TICVAI task descriptions into OpenProject, on the server (OpenProject 10, Docker container "openproject").
#
# The file comes from tools/op-descriptions.py: {work package id: markdown}. Written with update_columns, so:
#   - no notification email per ticket (through the API, 2,816 edits would mail every assignee 2,816 times over)
#   - no journal entry, so the Activity tab does not show the change; the description itself is what everyone reads
#   - updated_at is moved with it, or OpenProject's cached API answer keeps the old text
# Only work packages in project 153 are touched, and only their description. Dry run unless APPLY=1.
#
#   docker cp /tmp/op-descriptions.rb openproject:/tmp/ && docker cp /tmp/op-descriptions.json openproject:/tmp/
#   dry run:  docker exec openproject bash -c 'cd /app && bundle exec rails runner /tmp/op-descriptions.rb /tmp/op-descriptions.json'
#   status-aware (rewrite New, comment on the rest, retitle): add -e MODE=status -e SUBJECTS=/tmp/op-subjects.json
#   apply:    docker exec -e APPLY=1 openproject bash -c 'cd /app && bundle exec rails runner /tmp/op-descriptions.rb /tmp/op-descriptions.json'

PROJECT_ID = 153
path = ARGV[0] or abort("usage: rails runner op-descriptions.rb op-descriptions.json")
texts = JSON.parse(File.read(path)).transform_keys(&:to_i)
apply = ENV["APPLY"] == "1"

current = WorkPackage.where(id: texts.keys).pluck(:id, :project_id, :description).map { |i, p, d| [i, [p, d]] }.to_h
missing = texts.keys - current.keys
abort("work packages not found: #{missing.first(20).join(', ')}") if missing.any?
foreign = current.reject { |_, (p, _)| p == PROJECT_ID }.keys
abort("not in project #{PROJECT_ID}: #{foreign.first(20).join(', ')}") if foreign.any?

changed = texts.reject { |i, t| current[i][1].to_s.strip == t.strip }
puts "OpenProject #{OpenProject::VERSION}: #{texts.size} descriptions in the file, #{changed.size} differ from " \
     "what is there, #{texts.size - changed.size} already the same"
sample = changed.keys.first
puts "e.g. ##{sample}: #{current[sample][1].to_s.size} -> #{changed[sample].size} characters" if sample
exit unless apply

started = Time.now
# updated_at moves too: OpenProject caches each work package's API representation on it, so without this
# the API and the web page keep serving the old description (seen 24 September).
now = Time.now

# MODE=status (after the Block A audit, 28 September): only a ticket nobody has started gets its description
# rewritten. A ticket in progress, on hold, in QA or closed keeps the description its work was done against and
# gets the new text as one comment instead - rewriting it would change what someone is building to, or what QA
# already passed, without a trace. Comments are written with notifications off.
if ENV["MODE"] == "status"
  statuses = WorkPackage.where(id: changed.keys).includes(:status).map { |w| [w.id, w.status.name] }.to_h
  rewrite = changed.select { |i, _| statuses[i] == "New" }
  comment = changed.reject { |i, _| statuses[i] == "New" }
  puts "MODE=status: #{rewrite.size} New tickets rewritten, #{comment.size} started or closed tickets get a comment " \
       "(#{comment.keys.map { |i| statuses[i] }.tally.map { |s, n| "#{s} #{n}" }.join(', ')})"
  subjects = ENV["SUBJECTS"] && File.exist?(ENV["SUBJECTS"]) ? JSON.parse(File.read(ENV["SUBJECTS"])).transform_keys(&:to_i) : {}
  puts "retitles: #{subjects.size}" if subjects.any?
  exit unless apply

  author = User.find_by(login: ENV["AUTHOR"] || "admin") || User.where(admin: true).first
  WorkPackage.transaction do
    rewrite.each { |i, t| WorkPackage.where(id: i).update_all(description: t, updated_at: now) }
    subjects.each { |i, s| WorkPackage.where(id: i, project_id: PROJECT_ID).update_all(subject: s, updated_at: now) }
  end
  note = ->(t) { "**Ticket text updated after the Block A audit.** The description above is what this work " \
                 "started against; this is the current text.\n\n#{t}" }
  quiet = defined?(Journal::NotificationConfiguration) ? Journal::NotificationConfiguration.method(:with) : nil
  comment.each do |i, t|
    wp = WorkPackage.find(i)
    write = lambda do
      wp.add_journal(author, note.call(t))
      wp.save!(validate: false)
    end
    quiet ? quiet.call(false, &write) : write.call
  end
  puts "done: #{rewrite.size} rewritten, #{comment.size} commented, #{subjects.size} retitled " \
       "in #{(Time.now - started).round(1)}s"
  exit
end

WorkPackage.transaction do
  changed.each { |i, t| WorkPackage.where(id: i).update_all(description: t, updated_at: now) }
end
puts "done: #{changed.size} descriptions written in #{(Time.now - started).round(1)}s"
