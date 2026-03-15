

(define (problem BW-rand-10)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 )
(:init
(arm-empty)
(on b1 b6)
(on b2 b4)
(on b3 b7)
(on b4 b9)
(on b5 b3)
(on b6 b5)
(on-table b7)
(on-table b8)
(on b9 b1)
(on-table b10)
(clear b2)
(clear b8)
(clear b10)
)
(:goal
(and
(on b1 b9)
(on b2 b10)
(on b6 b3)
(on b8 b7)
(on b10 b1))
)
)


