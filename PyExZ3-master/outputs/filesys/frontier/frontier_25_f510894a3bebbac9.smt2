(set-logic ALL)
; Frontier Constraint ID: f510894a3bebbac9
; Generated at: 2026-04-16 15:43:19
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1498)) (False)
(assert (not (= x 1498)))

; Query: ((== x 1499)) (False)
(assert (not (not (= x 1499))))

(check-sat)
(get-model)
