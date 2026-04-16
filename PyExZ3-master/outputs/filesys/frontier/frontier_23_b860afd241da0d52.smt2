(set-logic ALL)
; Frontier Constraint ID: b860afd241da0d52
; Generated at: 2026-04-16 14:40:10
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 445)) (False)
(assert (not (= x 445)))

; Query: ((== x 446)) (False)
(assert (not (not (= x 446))))

(check-sat)
(get-model)
