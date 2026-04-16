(set-logic ALL)
; Constraint ID: ac147d24bcfbfc37
; Generated at: 2026-04-16 10:45:36
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59557)) (False)
(assert (not (not (= x 59557))))

(check-sat)
(get-model)
