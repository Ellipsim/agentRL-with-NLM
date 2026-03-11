

(define (problem BW-rand-10)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 )
(:init
(arm-empty)
(on b1 b8)
(on b2 b9)
(on-table b3)
(on-table b4)
(on-table b5)
(on b6 b10)
(on b7 b1)
(on b8 b4)
(on b9 b6)
(on b10 b7)
(clear b2)
(clear b3)
(clear b5)
)
(:goal
(and
(on b1 b5)
(on b4 b9)
(on b5 b4)
(on b6 b7)
(on b9 b3))
)
)


