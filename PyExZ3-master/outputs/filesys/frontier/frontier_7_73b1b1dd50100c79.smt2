(set-logic ALL)
; Frontier Constraint ID: 73b1b1dd50100c79
; Generated at: 2026-04-16 14:36:25
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 346)) (False)
(assert (not (= x 346)))

; Query: ((== x 347)) (False)
(assert (not (not (= x 347))))

(check-sat)
(get-model)
