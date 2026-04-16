(set-logic ALL)
; Frontier Constraint ID: 1085ab1643c97c1a
; Generated at: 2026-04-16 15:10:06
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1024)) (False)
(assert (not (= x 1024)))

; Query: ((== x 1025)) (False)
(assert (not (not (= x 1025))))

(check-sat)
(get-model)
