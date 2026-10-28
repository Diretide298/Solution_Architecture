// How the Tasks page counts a Task that has sub tasks (ticket-kinds.js
// `rollUp`), held to the rule the page states. Needs no viewer: it imports the
// module the page and My work share and asks it directly.
//
//   node checks/tasks-rollup-check.mjs
//
// The case it exists for (29 October): Sanket read 1 of 65 finished while nine
// of his sub tasks were Ready for QA, because the Tasks above them were New.
import {
  learnStatuses, rollUp, kindOf, isFinished, isAwaiting, isDone, isOpenWork, count,
} from '../public/ticket-kinds.js';

let ok = 0, bad = 0;
const check = (n, c, d = '') => { console.log(`${c ? 'PASS' : 'FAIL'}  ${n}${d ? ` — ${d}` : ''}`); c ? ok++ : bad++; };

// TICVAI's statuses, as the service hands them over.
learnStatuses([
  { name: 'New', isClosed: false, isDefault: true },
  { name: 'In progress', isClosed: false },
  { name: 'On hold', isClosed: false },
  { name: 'Ready for QA', isClosed: false },
  { name: 'Test failed', isClosed: false },
  { name: 'Closed', isClosed: true },
  { name: 'Rejected', isClosed: true },
]);
const task = (status = 'New') => ({ key: 't', type: 'Task', status });
const subs = (...statuses) => statuses.map((status, i) => ({ key: `s${i}`, type: 'Sub Task', status }));
/** The Task as the page counts it: the copy `asTask` makes. */
const counted = (t, list) => { const r = rollUp(t, list); return r ? { ...t, stage: r.stage, rolled: r } : t; };

check('no sub tasks: the Task is its own status', rollUp(task(), []) === null);
check('only rejected sub tasks: still its own status', rollUp(task(), subs('Rejected', 'Rejected')) === null);

let t = counted(task(), subs('Ready for QA', 'Ready for QA', 'Closed'));
check('every sub task finished, one still waiting: the Task waits for QA',
  kindOf(t) === 'qa' && isAwaiting(t) && isFinished(t), kindOf(t));
t = counted(task(), subs('Closed', 'Closed'));
check('every sub task closed: the Task is closed and done', kindOf(t) === 'done' && isDone(t), kindOf(t));
t = counted(task(), subs('Closed', 'Ready for QA', 'Rejected'));
check('a rejected sub task does not hold it back', isFinished(t), kindOf(t));
check('and is not counted in the roll-up', t.rolled.of === 2 && t.rolled.finished === 2, JSON.stringify(t.rolled));

t = counted(task(), subs('Ready for QA', 'New'));
check('some finished, some not begun: in progress, not finished', kindOf(t) === 'going' && !isFinished(t), kindOf(t));
t = counted(task(), subs('On hold', 'New'));
check('a sub task on hold has started: in progress', kindOf(t) === 'going', kindOf(t));
t = counted(task(), subs('New', 'New'));
check('nothing begun: not started', kindOf(t) === 'fresh', kindOf(t));
t = counted(task(), subs('Test failed', 'Closed'));
check('a sub task back from QA is not finished', !isFinished(t) && isOpenWork(t), kindOf(t));

t = counted(task('Closed'), subs('New'));
check('a Task closed in its own right stays closed', kindOf(t) === 'done', kindOf(t));
t = counted(task('Ready for QA'), subs('New'));
check('a Task waiting for QA in its own right stays waiting', kindOf(t) === 'qa', kindOf(t));
t = counted(task('On hold'), subs('In progress', 'New'));
check('a Task on hold with work under way stays on hold', kindOf(t) === 'stalled', kindOf(t));
t = counted(task('On hold'), subs('Closed', 'Ready for QA'));
check('but is finished once every sub task is', kindOf(t) === 'qa', kindOf(t));
t = counted(task('Rejected'), subs('Closed'));
check('a rejected Task stays rejected', kindOf(t) === 'rejected', kindOf(t));

// The Sanket case, in miniature: one Task finished on its own, and nine Tasks
// whose sub tasks are all Ready for QA. By status alone 1 of 10 is finished.
const own = [task('Closed'), ...Array.from({ length: 9 }, () => task('New'))];
const byStatus = count(own);
const rolled = count([own[0], ...own.slice(1).map((x) => counted(x, subs('Ready for QA', 'Ready for QA')))]);
check('by status alone the Tasks say 1 finished', byStatus.finished === 1, JSON.stringify(byStatus));
check('rolled up they say 10', rolled.finished === 10 && rolled.qa === 9, JSON.stringify(rolled));

// The Tickets count never sees a stage: the original object is untouched.
const original = task();
counted(original, subs('Closed'));
check('rolling up leaves the Task itself as OpenProject has it', !('stage' in original) && kindOf(original) === 'fresh');

console.log(`${ok} passed, ${bad} failed`);
process.exit(bad ? 1 : 0);
