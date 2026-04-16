(set-logic ALL)
; Frontier Constraint ID: b21a3963d6b58d29
; Generated at: 2026-04-16 13:27:43
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((> x 0)) (False)
(assert (not (> x 0)))

; Query: ((< x 0)) (False)
(assert (not (not (< x 0))))

(check-sat)
(get-model)
