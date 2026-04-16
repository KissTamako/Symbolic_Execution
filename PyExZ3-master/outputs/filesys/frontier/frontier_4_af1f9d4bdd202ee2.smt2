(set-logic ALL)
; Constraint ID: af1f9d4bdd202ee2
; Generated at: 2026-04-16 11:42:36
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60217)) (False)
(assert (not (not (= x 60217))))

(check-sat)
(get-model)
