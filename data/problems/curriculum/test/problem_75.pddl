

(define (problem BW-rand-10)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 )
(:init
(arm-empty)
(on-table b1)
(on-table b2)
(on b3 b4)
(on-table b4)
(on b5 b8)
(on b6 b10)
(on b7 b3)
(on b8 b9)
(on b9 b6)
(on-table b10)
(clear b1)
(clear b2)
(clear b5)
(clear b7)
)
(:goal
(and
(on b1 b8)
(on b2 b4)
(on b6 b5)
(on b8 b6)
(on b9 b7)
(on b10 b2))
)
)


