

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(on b1 b9)
(on b2 b11)
(on b3 b2)
(ontable b4)
(ontable b5)
(on b6 b8)
(on b7 b4)
(on b8 b7)
(on b9 b12)
(on b10 b1)
(ontable b11)
(ontable b12)
(clear b3)
(clear b5)
(clear b6)
(clear b10)
)
(:goal
(and
(on b1 b9)
(on b4 b8)
(on b5 b6)
(on b6 b1)
(on b7 b3)
(on b8 b12)
(on b11 b4)
(on b12 b7))
)
)


