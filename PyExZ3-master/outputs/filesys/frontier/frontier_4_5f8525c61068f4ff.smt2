(set-logic ALL)
; Constraint ID: 5f8525c61068f4ff
; Generated at: 2026-04-16 11:31:08
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60067)) (False)
(assert (not (not (= x 60067))))

(check-sat)
(get-model)
