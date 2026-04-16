(set-logic ALL)
; Frontier Constraint ID: bdba477d73c3bcc9
; Generated at: 2026-04-17 03:12:47
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 2848)) (False)
(assert (not (= x 2848)))

; Query: ((== x 2849)) (False)
(assert (not (not (= x 2849))))

(check-sat)
(get-model)
