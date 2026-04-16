(set-logic ALL)
; Frontier Constraint ID: 59e0585d40130e08
; Generated at: 2026-04-16 15:10:06
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1033)) (False)
(assert (not (= x 1033)))

; Query: ((== x 1034)) (False)
(assert (not (not (= x 1034))))

(check-sat)
(get-model)
