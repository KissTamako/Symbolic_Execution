(set-logic ALL)
; Frontier Constraint ID: 2ad5868b45c8da8d
; Generated at: 2026-04-16 15:10:06
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1027)) (False)
(assert (not (not (= x 1027))))

(check-sat)
(get-model)
