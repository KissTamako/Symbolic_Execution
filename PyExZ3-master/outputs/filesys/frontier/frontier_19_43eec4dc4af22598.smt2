(set-logic ALL)
; Frontier Constraint ID: 43eec4dc4af22598
; Generated at: 2026-04-16 15:26:57
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1339)) (False)
(assert (not (= x 1339)))

; Query: ((== x 1340)) (False)
(assert (not (not (= x 1340))))

(check-sat)
(get-model)
