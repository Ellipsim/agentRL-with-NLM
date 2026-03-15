

(define (problem BW-rand-10)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 )
(:init
(arm-empty)
(on b1 b4)
(on b2 b5)
(on-table b3)
(on b4 b8)
(on b5 b1)
(on b6 b7)
(on b7 b10)
(on-table b8)
(on-table b9)
(on b10 b2)
(clear b3)
(clear b6)
(clear b9)
)
(:goal
(and
(on b2 b4)
(on b3 b10)
(on b4 b5)
(on b5 b9)
(on b7 b8)
(on b9 b3)
(on b10 b6))
)
)


