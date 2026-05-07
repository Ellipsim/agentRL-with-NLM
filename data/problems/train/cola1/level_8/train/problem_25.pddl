

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(ontable b1)
(ontable b2)
(ontable b3)
(on b4 b7)
(on b5 b1)
(on b6 b10)
(on b7 b2)
(on b8 b5)
(on b9 b3)
(on b10 b8)
(clear b4)
(clear b6)
(clear b9)
)
(:goal
(and
(on b1 b3)
(on b3 b2)
(on b4 b8)
(on b5 b1)
(on b6 b10)
(on b7 b6)
(on b8 b5)
(on b9 b4))
)
)


