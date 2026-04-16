(set-logic ALL)
; Frontier Constraint ID: f363a37447f2860d
; Generated at: 2026-04-16 14:41:51
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 502)) (False)
(assert (not (not (= x 502))))

(check-sat)
(get-model)
