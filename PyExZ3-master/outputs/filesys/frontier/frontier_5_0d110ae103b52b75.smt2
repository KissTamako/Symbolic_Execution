(set-logic ALL)
; Frontier Constraint ID: 0d110ae103b52b75
; Generated at: 2026-04-17 01:52:09
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1843)) (False)
(assert (not (= x 1843)))

; Query: ((== x 1844)) (False)
(assert (not (not (= x 1844))))

(check-sat)
(get-model)
