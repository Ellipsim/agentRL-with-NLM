

(define (problem BW-rand-10)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 )
(:init
(arm-empty)
(on b1 b7)
(on b2 b9)
(on b3 b6)
(on-table b4)
(on-table b5)
(on b6 b1)
(on b7 b5)
(on b8 b2)
(on b9 b3)
(on b10 b8)
(clear b4)
(clear b10)
)
(:goal
(and
(on b1 b10)
(on b4 b6)
(on b5 b9)
(on b6 b8)
(on b7 b1)
(on b8 b2)
(on b9 b3))
)
)


