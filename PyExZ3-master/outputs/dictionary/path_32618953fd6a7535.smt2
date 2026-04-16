(set-logic ALL)
; Executed Path ID: 32618953fd6a7535
; Generated at: 2026-04-16 16:02:52
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: False

(declare-const in1 Int)

; ((== in1 3)) (True)
(assert (= in1 3))

(check-sat)
(get-model)
