

(define (problem BW-rand-10)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 )
(:init
(arm-empty)
(on b1 b9)
(on-table b2)
(on-table b3)
(on b4 b1)
(on b5 b3)
(on-table b6)
(on b7 b8)
(on b8 b6)
(on-table b9)
(on-table b10)
(clear b2)
(clear b4)
(clear b5)
(clear b7)
(clear b10)
)
(:goal
(and
(on b1 b6)
(on b4 b9)
(on b5 b8)
(on b6 b4)
(on b7 b2)
(on b8 b1)
(on b9 b7))
)
)


