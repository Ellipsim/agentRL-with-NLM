

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b8)
(on b2 b10)
(on b3 b7)
(on b4 b2)
(on b5 b1)
(on b6 b4)
(ontable b7)
(on b8 b9)
(ontable b9)
(on b10 b3)
(clear b5)
(clear b6)
)
(:goal
(and
(on b1 b7)
(on b2 b1)
(on b4 b3)
(on b5 b2)
(on b6 b10)
(on b7 b4)
(on b8 b9))
)
)


