(set-logic ALL)
; Frontier Constraint ID: 6efc034a36223a70
; Generated at: 2026-04-16 14:57:49
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 892)) (False)
(assert (not (= x 892)))

; Query: ((== x 893)) (False)
(assert (not (not (= x 893))))

(check-sat)
(get-model)
