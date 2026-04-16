(set-logic ALL)
; Frontier Constraint ID: c84ee6060fff9baa
; Generated at: 2026-04-16 14:43:36
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 667)) (False)
(assert (not (= x 667)))

; Query: ((== x 668)) (False)
(assert (not (not (= x 668))))

(check-sat)
(get-model)
