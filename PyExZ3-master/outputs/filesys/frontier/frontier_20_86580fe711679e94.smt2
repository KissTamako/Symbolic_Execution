(set-logic ALL)
; Frontier Constraint ID: 86580fe711679e94
; Generated at: 2026-04-16 14:36:25
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 367)) (False)
(assert (not (not (= x 367))))

(check-sat)
(get-model)
