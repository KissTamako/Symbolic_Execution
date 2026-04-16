(set-logic ALL)
; Frontier Constraint ID: 995a1a7f06468279
; Generated at: 2026-04-16 14:57:49
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 871)) (False)
(assert (not (= x 871)))

; Query: ((== x 872)) (False)
(assert (not (not (= x 872))))

(check-sat)
(get-model)
