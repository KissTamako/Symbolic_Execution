(set-logic ALL)
; Constraint ID: ce077fb9a91e5d51
; Generated at: 2026-04-16 10:43:23
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59473)) (False)
(assert (not (= x 59473)))

; Query: ((== x 59474)) (False)
(assert (not (not (= x 59474))))

(check-sat)
(get-model)
