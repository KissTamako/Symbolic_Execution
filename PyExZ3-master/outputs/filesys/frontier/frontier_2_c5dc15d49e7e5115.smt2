(set-logic ALL)
; Constraint ID: c5dc15d49e7e5115
; Generated at: 2026-04-16 11:00:46
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59614)) (False)
(assert (not (not (= x 59614))))

(check-sat)
(get-model)
