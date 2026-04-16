(set-logic ALL)
; Frontier Constraint ID: 054f362c77444133
; Generated at: 2026-04-17 01:52:09
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1852)) (False)
(assert (not (= x 1852)))

; Query: ((== x 1853)) (False)
(assert (not (not (= x 1853))))

(check-sat)
(get-model)
