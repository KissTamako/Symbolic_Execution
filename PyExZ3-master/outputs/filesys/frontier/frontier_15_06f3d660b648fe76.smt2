(set-logic ALL)
; Frontier Constraint ID: 06f3d660b648fe76
; Generated at: 2026-04-16 14:41:51
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 508)) (False)
(assert (not (= x 508)))

; Query: ((== x 509)) (False)
(assert (not (not (= x 509))))

(check-sat)
(get-model)
