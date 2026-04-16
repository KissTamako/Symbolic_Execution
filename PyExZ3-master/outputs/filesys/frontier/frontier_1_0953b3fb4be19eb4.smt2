(set-logic ALL)
; Frontier Constraint ID: 0953b3fb4be19eb4
; Generated at: 2026-04-16 16:02:53
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1687)) (False)
(assert (not (= x 1687)))

; Query: ((== x 1688)) (False)
(assert (not (not (= x 1688))))

(check-sat)
(get-model)
