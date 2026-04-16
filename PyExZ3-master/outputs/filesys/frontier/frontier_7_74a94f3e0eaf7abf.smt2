(set-logic ALL)
; Frontier Constraint ID: 74a94f3e0eaf7abf
; Generated at: 2026-04-16 14:44:34
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 721)) (False)
(assert (not (= x 721)))

; Query: ((== x 722)) (False)
(assert (not (not (= x 722))))

(check-sat)
(get-model)
