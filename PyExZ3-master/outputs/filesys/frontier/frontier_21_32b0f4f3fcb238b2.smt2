(set-logic ALL)
; Frontier Constraint ID: 32b0f4f3fcb238b2
; Generated at: 2026-04-16 15:16:56
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1192)) (False)
(assert (not (= x 1192)))

; Query: ((== x 1193)) (False)
(assert (not (not (= x 1193))))

(check-sat)
(get-model)
