(set-logic ALL)
; Constraint ID: 55ae3c6d75b4124b
; Generated at: 2026-04-16 11:40:22
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60163)) (False)
(assert (not (not (= x 60163))))

(check-sat)
(get-model)
