(set-logic ALL)
; Frontier Constraint ID: 8bf685445bf85310
; Generated at: 2026-04-17 01:52:09
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1867)) (False)
(assert (not (= x 1867)))

; Query: ((== x 1868)) (False)
(assert (not (not (= x 1868))))

(check-sat)
(get-model)
