(set-logic ALL)
; Frontier Constraint ID: 5bb3f2063548a247
; Generated at: 2026-04-16 15:56:50
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1615)) (False)
(assert (not (= x 1615)))

; Query: ((== x 1616)) (False)
(assert (not (not (= x 1616))))

(check-sat)
(get-model)
