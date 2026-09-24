# Insert the TICVAI "follows" links on the OpenProject server (OpenProject 10, Docker container "openproject").
#
# Why on the server: through the API each link takes ~40 s once the graph is large. The links file comes from
# tools/op-bulk-links.py, which has already checked every id and that the graph has no cycle, so the per-link
# validation (a walk of the whole graph) is skipped here.
#
# What is NOT skipped: OpenProject 10 keeps every derived connection in the relations table too (the typed_dag
# closure: follows=2..n rows, and "mixed" rows through parents and sub-tasks). Each link is saved through the
# Relation model, so its callbacks write those rows exactly as a link made in the UI would. That work is most of
# the cost, so this is faster than the API but not instant; LIMIT times a few links first.
#
# Safe to run more than once: a link already there as a DIRECT link (follows = 1, hierarchy = 0) is skipped.
# Derived rows (follows > 1, or mixed with hierarchy) do not count as existing. Each link commits on its own, so
# stopping part-way keeps what was made.
#
#   docker cp /tmp/op-bulk-links.rb openproject:/tmp/ && docker cp /tmp/op-links.json openproject:/tmp/
#   dry run:     docker exec openproject bash -c 'cd /app && bundle exec rails runner /tmp/op-bulk-links.rb /tmp/op-links.json'
#   time five:   docker exec -e APPLY=1 -e LIMIT=5 openproject bash -c 'cd /app && bundle exec rails runner /tmp/op-bulk-links.rb /tmp/op-links.json'
#   the rest:    docker exec -e APPLY=1 openproject bash -c 'cd /app && bundle exec rails runner /tmp/op-bulk-links.rb /tmp/op-links.json'

PROJECT_ID = 153
path = ARGV[0] or abort("usage: rails runner op-bulk-links.rb op-links.json")
pairs = JSON.parse(File.read(path))
apply = ENV["APPLY"] == "1"
limit = ENV["LIMIT"]&.to_i

ids = pairs.flatten.uniq
wps = WorkPackage.where(id: ids).pluck(:id, :project_id).to_h
missing = ids - wps.keys
abort("work packages not found: #{missing.first(20).join(', ')}") if missing.any?
foreign = wps.reject { |_, p| p == PROJECT_ID }.keys
abort("not in project #{PROJECT_ID}: #{foreign.first(20).join(', ')}") if foreign.any?

direct = Relation.where(from_id: ids, to_id: ids, follows: 1, hierarchy: 0, relates: 0, duplicates: 0,
                        blocks: 0, includes: 0, requires: 0)
existing = direct.pluck(:from_id, :to_id).to_set
todo = pairs.reject { |f, t| existing.include?([f, t]) }
rows_before = Relation.count
puts "OpenProject #{OpenProject::VERSION}: #{pairs.size} links in the file, #{pairs.size - todo.size} already " \
     "there as direct links, #{todo.size} to add (relations table: #{rows_before} rows)"
exit unless apply

todo = todo.first(limit) if limit
made = 0
started = Time.now
todo.each do |from_id, to_id|
  t = Time.now
  r = Relation.new(from_id: from_id, to_id: to_id)
  r.relation_type = Relation::TYPE_FOLLOWS
  r.save!(validate: false)
  made += 1
  if limit || (made % 25).zero?
    puts "  #{made}/#{todo.size}: ##{from_id} follows ##{to_id} in #{(Time.now - t).round(1)}s " \
         "(#{(Time.now - started).round}s so far)"
  end
end
row = Relation.where(from_id: todo.last[0], to_id: todo.last[1]).first&.attributes&.slice("follows", "hierarchy", "count")
puts "done: #{made} links in #{(Time.now - started).round}s; relations table #{rows_before} -> #{Relation.count} rows; " \
     "last link stored as #{row.inspect} (expect follows 1, hierarchy 0, count 1)"
