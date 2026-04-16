(set-logic ALL)
; Constraint ID: e0b3d4f8fdffd02f
; Generated at: 2026-04-16 11:00:46
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59629)) (False)
(assert (not (not (= x 59629))))

(check-sat)
(get-model)
