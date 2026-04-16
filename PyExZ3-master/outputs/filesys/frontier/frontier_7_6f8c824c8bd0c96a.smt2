(set-logic ALL)
; Frontier Constraint ID: 6f8c824c8bd0c96a
; Generated at: 2026-04-17 03:12:47
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 2821)) (False)
(assert (not (= x 2821)))

; Query: ((== x 2822)) (False)
(assert (not (not (= x 2822))))

(check-sat)
(get-model)
