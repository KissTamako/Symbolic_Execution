(set-logic ALL)
; Frontier Constraint ID: c48733833aa41aca
; Generated at: 2026-04-16 15:16:56
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1165)) (False)
(assert (not (= x 1165)))

; Query: ((== x 1166)) (False)
(assert (not (not (= x 1166))))

(check-sat)
(get-model)
