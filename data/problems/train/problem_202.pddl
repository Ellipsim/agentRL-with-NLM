

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(ontable b1)
(on b2 b1)
(on b3 b4)
(on b4 b2)
(on b5 b9)
(ontable b6)
(on b7 b6)
(on b8 b10)
(ontable b9)
(ontable b10)
(clear b3)
(clear b5)
(clear b7)
(clear b8)
)
(:goal
(and
(on b1 b7)
(on b5 b6)
(on b6 b4)
(on b7 b3)
(on b8 b2)
(on b9 b5))
)
)


