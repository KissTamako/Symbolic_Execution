(set-logic ALL)
; Constraint ID: 82c39812f12b0686
; Generated at: 2026-04-16 11:40:22
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60136)) (False)
(assert (not (not (= x 60136))))

(check-sat)
(get-model)
