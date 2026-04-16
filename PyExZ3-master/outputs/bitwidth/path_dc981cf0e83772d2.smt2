(set-logic ALL)
; Path ID: dc981cf0e83772d2
; Generated at: 2026-04-16 12:01:20
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const a Int)
(declare-const se Int)


; Query: ((< (+ a 1) a)) (False)
(assert (not (not (< (+ a 1) a))))

(check-sat)
(get-model)
