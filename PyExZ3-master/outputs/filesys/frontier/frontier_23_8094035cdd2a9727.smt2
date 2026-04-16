(set-logic ALL)
; Frontier Constraint ID: 8094035cdd2a9727
; Generated at: 2026-04-17 01:52:09
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1870)) (False)
(assert (not (= x 1870)))

; Query: ((== x 1871)) (False)
(assert (not (not (= x 1871))))

(check-sat)
(get-model)
