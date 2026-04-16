(set-logic ALL)
; Frontier Constraint ID: 9a5433bbe8071c74
; Generated at: 2026-04-16 15:26:57
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1321)) (False)
(assert (not (= x 1321)))

; Query: ((== x 1322)) (False)
(assert (not (not (= x 1322))))

(check-sat)
(get-model)
